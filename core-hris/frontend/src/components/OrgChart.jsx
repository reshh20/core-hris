import { useCallback, useMemo, useState, useEffect } from 'react';
import {
  ReactFlow,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import EmployeeNode from './EmployeeNode';
import LoadingState from './LoadingState';
import EmptyState from './EmptyState';
import ErrorState from './ErrorState';
import { fetchOrgChart } from '../services/organizationService';

const NODE_WIDTH = 220;
const NODE_HEIGHT = 80;
const HORIZONTAL_GAP = 40;
const VERTICAL_GAP = 100;

/**
 * Calculate the width of a subtree (in terms of leaf nodes).
 */
function getSubtreeWidth(node) {
  if (!node.children || node.children.length === 0) {
    return NODE_WIDTH;
  }
  const childrenWidth = node.children.reduce(
    (sum, child) => sum + getSubtreeWidth(child) + HORIZONTAL_GAP,
    -HORIZONTAL_GAP
  );
  return Math.max(NODE_WIDTH, childrenWidth);
}

/**
 * Build React Flow nodes and edges from the nested org chart data.
 */
function buildNodesAndEdges(orgData) {
  const nodes = [];
  const edges = [];

  function processNode(node, x, y) {
    const nodeId = `node-${node.id}`;

    nodes.push({
      id: nodeId,
      type: 'employeeNode',
      position: { x, y },
      data: {
        firstName: node.first_name,
        lastName: node.last_name,
        positionTitle: node.position_title,
        departmentName: node.department_name,
        profileImage: node.profile_image,
        employeeId: node.id,
      },
    });

    if (node.children && node.children.length > 0) {
      const totalWidth = node.children.reduce(
        (sum, child) => sum + getSubtreeWidth(child) + HORIZONTAL_GAP,
        -HORIZONTAL_GAP
      );

      let currentX = x + NODE_WIDTH / 2 - totalWidth / 2;

      node.children.forEach((child) => {
        const childWidth = getSubtreeWidth(child);
        const childX = currentX + childWidth / 2 - NODE_WIDTH / 2;
        const childY = y + NODE_HEIGHT + VERTICAL_GAP;

        const childNodeId = `node-${child.id}`;
        edges.push({
          id: `edge-${node.id}-${child.id}`,
          source: nodeId,
          target: childNodeId,
          type: 'smoothstep',
          style: { stroke: '#94a3b8', strokeWidth: 2 },
          animated: false,
        });

        processNode(child, childX, childY);
        currentX += childWidth + HORIZONTAL_GAP;
      });
    }
  }

  // Handle multiple root nodes
  let startX = 0;
  orgData.forEach((root) => {
    const width = getSubtreeWidth(root);
    processNode(root, startX, 0);
    startX += width + HORIZONTAL_GAP * 2;
  });

  return { nodes, edges };
}

const nodeTypes = { employeeNode: EmployeeNode };

export default function OrgChart() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEmpty, setIsEmpty] = useState(false);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchOrgChart();

      if (!data || data.length === 0) {
        setIsEmpty(true);
        setLoading(false);
        return;
      }

      const { nodes: flowNodes, edges: flowEdges } = buildNodesAndEdges(data);
      setNodes(flowNodes);
      setEdges(flowEdges);
      setIsEmpty(false);
    } catch (err) {
      setError(err.friendlyMessage || 'Failed to load organization chart');
    } finally {
      setLoading(false);
    }
  }, [setNodes, setEdges]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  if (loading) return <LoadingState message="Loading organization chart..." />;
  if (error) return <ErrorState message={error} onRetry={loadData} />;
  if (isEmpty) return <EmptyState title="No Organization Data" message="No employees found in the system to build the hierarchy." />;

  return (
    <div className="w-full h-[calc(100vh-180px)] bg-white rounded-xl border border-surface-200 shadow-sm overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.3 }}
        minZoom={0.2}
        maxZoom={1.5}
        defaultViewport={{ x: 0, y: 0, zoom: 0.7 }}
        proOptions={{ hideAttribution: true }}
      >
        <Controls
          showInteractive={false}
          className="bg-white border border-surface-200 rounded-lg shadow-sm"
        />
        <Background color="#e2e8f0" gap={20} size={1} />
      </ReactFlow>
    </div>
  );
}

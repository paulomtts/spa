import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ReactFlow,
  Controls,
  Background,
  applyNodeChanges,
  applyEdgeChanges,
  NodeChange,
  EdgeChange,
  Node,
  Edge,
  ReactFlowProvider,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

// Extend the Window interface to include our custom properties
interface CustomWindow extends Window {
  initialNodes?: Node[];
  initialEdges?: Edge[];
}

declare const window: CustomWindow;

const Flow = () => {
  const [nodes, setNodes] = useState<Node[]>(window.initialNodes || []);
  const [edges, setEdges] = useState<Edge[]>(window.initialEdges || []);

  const onNodesChange = (changes: NodeChange[]) =>
    setNodes((nds) => applyNodeChanges(changes, nds));

  const onEdgesChange = (changes: EdgeChange[]) =>
    setEdges((eds) => applyEdgeChanges(changes, eds));

  return (
    <ReactFlowProvider>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        defaultEdgeOptions={{
          style: { stroke: "#b1b1b7", strokeWidth: 2 },
          type: "smoothstep",
        }}
        proOptions={{ hideAttribution: true }}
      >
        <Controls />
        <Background />
      </ReactFlow>
    </ReactFlowProvider>
  );
};

const container = document.getElementById("flow-container");

if (container) {
  const root = createRoot(container);
  root.render(<Flow />);
}

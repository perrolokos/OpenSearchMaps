import ReactFlow, { Background, Controls } from 'reactflow'
import type { Node, Edge } from 'reactflow'
import 'reactflow/dist/style.css'
import { useStore } from '../store/useStore'
import { useMemo } from 'react'

export default function GraphCanvas() {
  const articles = useStore((s) => s.articles)
  const selectedId = useStore((s) => s.selectedId)
  const select = useStore((s) => s.select)

  const nodes = useMemo<Node[]>(
    () =>
      articles.map((a, idx) => ({
        id: String(a.id),
        position: { x: (idx % 5) * 150, y: Math.floor(idx / 5) * 100 },
        data: { label: a.title },
        style: {
          border: a.id === selectedId ? '2px solid #3b82f6' : undefined,
        },
      })),
    [articles, selectedId]
  )

  const edges: Edge[] = []

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      fitView
      onNodeClick={(_, node) => select(Number(node.id))}
    >
      <Background />
      <Controls />
    </ReactFlow>
  )
}

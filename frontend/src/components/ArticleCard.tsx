import { useStore } from '../store/useStore'
import type { Article } from '../types'

interface Props {
  article: Article
}

export default function ArticleCard({ article }: Props) {
  const selectedId = useStore((s) => s.selectedId)
  const select = useStore((s) => s.select)

  const isSelected = selectedId === article.id

  return (
    <div
      onClick={() => select(article.id)}
      className={`p-2 border-b cursor-pointer ${isSelected ? 'bg-blue-100 dark:bg-blue-900' : ''}`}
    >
      <h3 className="font-semibold">{article.title}</h3>
      <p className="text-sm text-gray-500">{article.authors}</p>
    </div>
  )
}

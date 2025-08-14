import { useEffect } from 'react'
import { api } from '../api/client'
import { useStore } from '../store/useStore'
import type { Article } from '../types'
import ArticleCard from './ArticleCard'

export default function ArticleList() {
  const articles = useStore((s) => s.articles)
  const setArticles = useStore((s) => s.setArticles)

  useEffect(() => {
    const fetchArticles = async () => {
      const { data } = await api.get<Article[]>('articles/')
      setArticles(data)
    }
    fetchArticles()
  }, [setArticles])

  return (
    <div className="overflow-y-auto h-full">
      {articles.map((a) => (
        <ArticleCard key={a.id} article={a} />
      ))}
    </div>
  )
}

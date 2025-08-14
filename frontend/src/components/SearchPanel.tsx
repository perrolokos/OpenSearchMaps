import { useState } from 'react'
import { api } from '../api/client'
import { useStore } from '../store/useStore'
import type { Article } from '../types'

export default function SearchPanel() {
  const [query, setQuery] = useState('')
  const setArticles = useStore((s) => s.setArticles)

  const search = async (e: React.FormEvent) => {
    e.preventDefault()
    const { data } = await api.get<Article[]>('articles/', { params: { search: query } })
    setArticles(data)
  }

  return (
    <form onSubmit={search} className="p-4 border-b border-gray-200 dark:border-gray-700">
      <input
        type="text"
        className="w-full p-2 rounded border"
        placeholder="Search articles..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
    </form>
  )
}

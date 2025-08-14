import { create } from 'zustand'
import type { Article } from '../types'

type State = {
  articles: Article[]
  selectedId: number | null
  setArticles: (articles: Article[]) => void
  select: (id: number | null) => void
}

export const useStore = create<State>((set) => ({
  articles: [],
  selectedId: null,
  setArticles: (articles) => set({ articles }),
  select: (id) => set({ selectedId: id }),
}))

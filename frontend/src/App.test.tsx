import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'

vi.mock('./components/ArticleList', () => ({ default: () => <div>Articles</div> }))
vi.mock('./components/GraphCanvas', () => ({ default: () => <div>Graph</div> }))

import App from './App'

describe('App', () => {
  it('renders sidebar and panels', () => {
    render(<App />)
    expect(screen.getByText(/OpenSearchMaps/)).toBeInTheDocument()
  })
})

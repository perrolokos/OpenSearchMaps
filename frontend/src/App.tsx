import Sidebar from './components/Sidebar'
import SearchPanel from './components/SearchPanel'
import ArticleList from './components/ArticleList'
import GraphCanvas from './components/GraphCanvas'

export default function App() {
  return (
    <div className="flex h-full">
      <Sidebar />
      <div className="flex flex-col flex-1">
        <SearchPanel />
        <div className="flex flex-1">
          <div className="w-1/3 border-r overflow-hidden">
            <ArticleList />
          </div>
          <div className="flex-1">
            <GraphCanvas />
          </div>
        </div>
      </div>
    </div>
  )
}

export default function Sidebar() {
  return (
    <aside className="w-64 bg-gray-100 dark:bg-gray-900 p-4 flex flex-col space-y-4">
      <h2 className="text-xl font-bold">OpenSearchMaps</h2>
      <nav className="flex-1">
        <ul className="space-y-2">
          <li className="text-gray-600 dark:text-gray-300">Workspaces</li>
          <li className="text-gray-600 dark:text-gray-300">Tags</li>
          <li className="text-gray-600 dark:text-gray-300">Account</li>
        </ul>
      </nav>
    </aside>
  )
}

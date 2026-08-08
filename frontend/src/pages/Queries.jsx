import { useState, useEffect } from 'react'
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Copy } from 'lucide-react'


function Queries() {
  const [queries, setQueries] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [queryName, setQueryName] = useState("")
  const [querySql, setQuerySql] = useState("")
  const [reportType, setReportType] = useState("")
  const [copiedId, setCopiedId] = useState(null)

  async function fetchQueries() {
    const token = localStorage.getItem("token")
    const response = await fetch("http://127.0.0.1:8000/queries", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
    const data = await response.json()
    setQueries(data)
  }

  async function handleCreateQuery() {
    const token = localStorage.getItem("token")
    const response = await fetch("http://127.0.0.1:8000/queries", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        query_name: queryName,
        query: querySql,
        report_type: reportType
      })
    })
    if (!response.ok) {
      console.log("Failed to create query")
      return
    }
    setShowForm(false)
    fetchQueries()
  }

  function handleCopy(query) {
  navigator.clipboard.writeText(query.query)
  setCopiedId(query.id)
  setTimeout(() => setCopiedId(null), 2000)
  }

  useEffect(() => {
    fetchQueries()
  }, [])

  return (
    <div className="p-8 pt-16 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">My Queries</h1>

      <Button onClick={() => setShowForm(true)} className="mb-6">Add Query</Button>

      {showForm && (
        <Card className="p-6 mb-6 shadow-sm">
          <h2 className="text-lg font-semibold mb-4">New Query</h2>
          <form onSubmit={(e) => { e.preventDefault(); handleCreateQuery(); }}>
            <Label className="p-2">Query Name</Label>
            <Input value={queryName} onChange={(e) => setQueryName(e.target.value)} className="mb-3" />

            <Label className="p-2">Report Type</Label>
            <Input value={reportType} onChange={(e) => setReportType(e.target.value)} className="mb-3" />

            <Label className="p-2">SQL</Label>
            <textarea
              value={querySql}
              onChange={(e) => setQuerySql(e.target.value)}
              className="w-full border rounded p-2 text-sm font-mono mb-3 h-32"
            />

            <div className="flex gap-2">
              <Button type="submit">Save</Button>
              <Button type="button" onClick={() => setShowForm(false)}>Cancel</Button>
            </div>
          </form>
        </Card>
      )}

      {!showForm && queries.length === 0 && (
        <p className="text-gray-500">No queries yet. Create your first one!</p>
      )}

      {queries.length > 0 && (  
        <div className="flex flex-col gap-4">
          {queries.map((query) => (
            <Card key={query.id} className="p-4 shadow-sm">
            <div className="flex justify-between items-center">
                <h2 className="text-lg font-semibold">{query.query_name}</h2>
                {copiedId === query.id && (
                <span className="text-xs text-black-600 font-medium">Query copied!</span>
                )}
            </div>
            <p className="text-sm text-gray-500 mt-1">{query.report_type}</p>
            <div className="relative">
                <pre className="bg-gray-100 rounded p-3 mt-3 text-sm overflow-x-auto">
                {query.query}
                </pre>
                <button
                onClick={() => handleCopy(query)}
                className="absolute bottom-2 right-2 p-1.5 rounded hover:bg-gray-200 transition-colors"
                >
                <Copy size={16} />
                </button>
            </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

export default Queries
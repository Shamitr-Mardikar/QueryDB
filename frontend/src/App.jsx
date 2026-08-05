import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Queries from './pages/Queries'
import Register from './pages/Register'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/queries" element={<Queries />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  )
}


export default App
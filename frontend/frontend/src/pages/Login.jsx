import { useState } from 'react'
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { useNavigate, Link } from 'react-router-dom'

function Login() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const navigate = useNavigate()

    async function handleLogin() {
        const formData = new URLSearchParams()
        formData.append("username", email)
        formData.append("password", password)

        const response = await fetch("http://127.0.0.1:8000/users/login", {
            method: "POST",
            headers: { 
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        })

        if (!response.ok) {
            console.log("login failed")
            return
        }

        const data = await response.json()
        localStorage.setItem("token", data.access_token)
        navigate("/queries")
        console.log("Logged In! Token: ", data.access_token)
    }

    return (
            <div className="min-h-screen flex flex-col items-center pt-16">
                <h1 className="text-2xl font-bold text-center pt-32 pb-4">Query DB</h1>
                <div className="mt-4">
                    <Card className="p-8 w-96 shadow-md">
                    <form onSubmit={(e) => { e.preventDefault(); handleLogin(); }}>
                        <Label htmlFor="email" className="p-1">Email</Label>
                        <Input 
                        id="email" 
                        type="email" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        />

                        <Label htmlFor="password" className="p-1 mt-3">Password</Label>
                        <Input 
                        id="password" 
                        type="password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        />

                        <Button type="submit" className="mt-4 w-24 mx-auto block hover:bg-gray-800 transition-colors rounded-full">
                        Login
                        </Button>
                    </form>
                    <p className="text-center mt-1 text-sm">
                        Don't have an Account?{" "}
                        <br />
                        <Link to="/register" className="text-black-600 hover:underline">
                        Click Here!
                        </Link>
                        </p>
                    </Card>
                </div>
            </div>
    )
}

export default Login
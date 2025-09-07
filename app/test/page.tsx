'use client'

import { useState } from 'react'

export default function TestAPI() {
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const testAPI = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    
    console.log('Environment check:')
    console.log('NODE_ENV:', process.env.NODE_ENV)
    console.log('NEXT_PUBLIC_API_URL:', process.env.NEXT_PUBLIC_API_URL)
    console.log('API_BASE_URL:', API_BASE_URL)

    try {
      // Test 1: Simple GET request
      console.log('Testing GET request to:', `${API_BASE_URL}/`)
      const getResponse = await fetch(`${API_BASE_URL}/`)
      console.log('GET Response status:', getResponse.status)
      console.log('GET Response headers:', Object.fromEntries(getResponse.headers.entries()))
      
      if (!getResponse.ok) {
        throw new Error(`GET request failed: ${getResponse.status}`)
      }
      
      const getData = await getResponse.json()
      console.log('GET Response data:', getData)

      // Test 2: POST request
      console.log('Testing POST request to:', `${API_BASE_URL}/api/generate-content`)
      const postResponse = await fetch(`${API_BASE_URL}/api/generate-content`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ 
          topic: 'test', 
          difficulty_level: 'beginner', 
          target_audience: 'students' 
        })
      })
      
      console.log('POST Response status:', postResponse.status)
      console.log('POST Response headers:', Object.fromEntries(postResponse.headers.entries()))
      
      if (!postResponse.ok) {
        throw new Error(`POST request failed: ${postResponse.status}`)
      }
      
      const postData = await postResponse.json()
      console.log('POST Response data:', postData)

      setResult({
        get: { status: getResponse.status, data: getData },
        post: { status: postResponse.status, data: postData }
      })

    } catch (err: any) {
      console.error('API Test Error:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">API Connection Test</h1>
        
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Environment Variables</h2>
          <div className="space-y-2">
            <p><strong>NODE_ENV:</strong> {process.env.NODE_ENV}</p>
            <p><strong>NEXT_PUBLIC_API_URL:</strong> {process.env.NEXT_PUBLIC_API_URL || 'Not set'}</p>
            <p><strong>API_BASE_URL:</strong> {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <button
            onClick={testAPI}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Testing...' : 'Test API Connection'}
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            <h3 className="font-bold">Error:</h3>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
            <h3 className="font-bold">Success!</h3>
            <pre className="mt-2 text-sm overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Instructions</h2>
          <ol className="list-decimal list-inside space-y-2">
            <li>Click "Test API Connection" button</li>
            <li>Open browser developer tools (F12)</li>
            <li>Check the Console tab for detailed logs</li>
            <li>Check the Network tab for HTTP requests</li>
            <li>Share any error messages you see</li>
          </ol>
        </div>
      </div>
    </div>
  )
}

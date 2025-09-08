import './globals.css'

export const metadata = {
  title: 'Vidya AI - Educational Content Generator',
  description: 'Generate educational videos with AI explanations, audio narration, and animated visuals',
}

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#3b82f6',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
// Deployment trigger - Mon Sep  8 09:21:48 AM IST 2025

// Improved token risk evaluation and UI binding

interface TokenData {
  // define expected shape here
  symbol: string
  price: number
  volume24h: number
  liquidity: number
  [key: string]: any
}

async function evaluateTokenRisk(tokenData: TokenData): Promise<string> {
  try {
    const risk = await riskRadar(tokenData)
    const volatility = await volatilityPredict(tokenData)
    return `${risk} | ${volatility}`
  } catch (err: any) {
    console.error("Risk evaluation failed:", err)
    return "Error evaluating risk"
  }
}

function showResult(text: string) {
  let output = document.getElementById("scan-result")
  if (!output) {
    output = document.createElement("div")
    output.id = "scan-result"
    output.className = "mt-4 p-3 bg-gray-100 dark:bg-gray-800 rounded"
    document.body.appendChild(output)
  }
  output.textContent = text
}

function bindUIEvents() {
  const scanBtn = document.getElementById("scan-button") as HTMLButtonElement | null
  if (!scanBtn) return

  scanBtn.addEventListener("click", async () => {
    scanBtn.disabled = true
    scanBtn.textContent = "Scanning..."
    try {
      const data = gatherTokenInput() as TokenData
      const result = await evaluateTokenRisk(data)
      showResult(result)
    } catch (err: any) {
      console.error("Scan error:", err)
      showResult("An unexpected error occurred")
    } finally {
      scanBtn.disabled = false
      scanBtn.textContent = "Scan Token"
    }
  })
}

// Initialize on DOM ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bindUIEvents)
} else {
  bindUIEvents()
}

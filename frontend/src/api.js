export async function fetchBusinessRules(formData) {
  const API_URL = "https://business-compliances.onrender.com";
  const response = await fetch(`${API_URL}/get-rules`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
  });
  if (!response.ok) {
    throw new Error("Failed to fetch business rules");
  }
  return await response.json();
}

export async function fetchBusinessRules(formData) {
  const response = await fetch("http://localhost:5000/get-rules", {
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

const form = document.getElementById("resumeForm");
const statusEl = document.getElementById("status");
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = new FormData(form);
  statusEl.textContent = "Analyzing resume...";
  try {
    const response = await fetch("/api/analyze", {method:"POST", body:data});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Analysis failed");
    renderResults(result);
    statusEl.textContent = "Analysis completed.";
  } catch (err) {
    statusEl.textContent = err.message;
  }
});

function renderResults(r) {
  document.getElementById("results").classList.remove("hidden");
  document.getElementById("resumeScore").textContent = r.resume_score;
  document.getElementById("atsScore").textContent = r.ats_score;
  document.getElementById("matchedCount").textContent = r.matched_skills.length;
  document.getElementById("missingCount").textContent = r.missing_skills.length;

  document.getElementById("skills").innerHTML =
    r.matched_skills.map(x => `<span class="pill">${x}</span>`).join("") +
    r.missing_skills.map(x => `<span class="pill missing">${x}</span>`).join("");

  document.getElementById("sections").innerHTML =
    Object.entries(r.sections).map(([k,v]) =>
      `<div class="check"><span>${k}</span><strong>${v ? "✓ Present" : "✗ Missing"}</strong></div>`
    ).join("");

  document.getElementById("suggestions").innerHTML =
    r.suggestions.map(x => `<li>${x}</li>`).join("");
}

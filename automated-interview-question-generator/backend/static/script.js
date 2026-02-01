async function generate() {
  const btn = document.getElementById("generateBtn");
  const loading = document.getElementById("loadingText");
  const output = document.getElementById("output");

  // UI: start loading
  btn.disabled = true;
  btn.innerText = "Generating…";
  loading.style.display = "block";
  output.innerHTML = "";

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        role: document.getElementById("role").value,
        skills: document.getElementById("skills").value,
        resume: document.getElementById("resume").value,
        num_questions: Number(document.getElementById("num").value)
      })
    });

    if (!res.ok) {
      throw new Error("Server error");
    }

    const data = await res.json();

    data.questions.forEach((q, index) => {
      const div = document.createElement("div");
      div.className = "question-card";

      div.innerHTML = `
        <h3>
  Q${index + 1}. ${q.question}
  <span style="
    margin-left: 8px;
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 999px;
    background: #eef2ff;
    color: #4f46e5;
    font-weight: 500;
  ">
    ${q.type.toUpperCase()}
  </span>
</h3>
        ${
          q.type === "mcq"
            ? q.options.map(opt => `<p>• ${opt}</p>`).join("")
            : ""
        }
        <p><strong>Answer:</strong> ${q.answer}</p>
        <p class="explanation"><strong>Explanation:</strong> ${q.explanation}</p>
      `;

      output.appendChild(div);
    });

  } catch (err) {
    output.innerHTML = "<p style='color:red;'>Something went wrong. Please try again.</p>";
  }

  // UI: stop loading
  btn.disabled = false;
  btn.innerText = "Generate Questions";
  loading.style.display = "none";
}

// ✅ Change this after deploying backend on Render
const API_URL = "https://potato-disease-yolov8-render.onrender.com";

const imageInput = document.getElementById("imageInput");
const predictBtn = document.getElementById("predictBtn");
const resultBox = document.getElementById("resultBox");
const previewImg = document.getElementById("previewImg");

imageInput.addEventListener("change", () => {
  if (imageInput.files.length > 0) {
    const file = imageInput.files[0];
    previewImg.src = URL.createObjectURL(file);
    previewImg.style.display = "block";
  }
});

predictBtn.addEventListener("click", async () => {
  if (!imageInput.files.length) {
    alert("Please select an image first!");
    return;
  }

  const file = imageInput.files[0];
  const formData = new FormData();
  formData.append("image", file);

  resultBox.innerHTML = "<p>⏳ Predicting... Please wait</p>";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (data.error) {
      resultBox.innerHTML = `<p>❌ Error: ${data.error}</p>`;
      return;
    }

    resultBox.innerHTML = `
      <h3>✅ Prediction Result</h3>
      <p><b>Class:</b> ${data.predicted_class}</p>
      <p><b>Confidence:</b> ${data.confidence}%</p>
      <p><b>Status:</b> ${data.status}</p>
      <p><b>Remedy:</b><br/> ${data.remedy}</p>
    `;
  } catch (err) {
    resultBox.innerHTML = `
      <p>❌ Failed to connect to backend.</p>
      <p><b>Tip:</b> Check your Render link in script.js</p>
    `;
  }
});

// ===== DOM Elements =====
const imageUpload = document.getElementById("imageUpload");
const previewImage = document.getElementById("previewImage");
const predictBtn = document.getElementById("predictBtn");
const loader = document.getElementById("loader");
const progressFill = document.getElementById("progress-fill");
const progressText = document.getElementById("progress-text");

let uploadedFile = null;

// ===== Upload & Preview =====
imageUpload.addEventListener("change", () => {
  uploadedFile = imageUpload.files[0];
  if (uploadedFile) {
    previewImage.src = URL.createObjectURL(uploadedFile);
    previewImage.classList.remove("hidden");
    predictBtn.disabled = false;
  }
});

// ===== Predict Button =====
predictBtn.addEventListener("click", async () => {
  if (!uploadedFile) return alert("Please upload an image first!");

  loader.classList.remove("hidden");
  predictBtn.disabled = true;

  let progress = 0;
  const interval = setInterval(() => {
    progress = Math.min(progress + 5, 95);
    progressFill.style.width = `${progress}%`;
    progressText.textContent = `${progress}%`;
  }, 100);

  const formData = new FormData();
  formData.append("file", uploadedFile);

  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    clearInterval(interval);
    progressFill.style.width = "100%";
    progressText.textContent = "100%";

    const hasDisease =
      data.disease && data.disease.toLowerCase() !== "healthy";

    // Redirect to result page with query params
    setTimeout(() => {
      const params = new URLSearchParams({
        imageName: uploadedFile.name,
        imagePath: URL.createObjectURL(uploadedFile),
        disease: data.disease,
        hasDisease,
      });
      window.location.href = `result.html?${params.toString()}`;
    }, 700);
  } catch (err) {
    clearInterval(interval);
    alert("⚠️ Error connecting to backend!");
    loader.classList.add("hidden");
    predictBtn.disabled = false;
  }
});

// ===== Fetch Community & Success Sections =====
async function fetchFrontendSections() {
  const endpoints = {
    community: "/community",
    success: "/success",
  };

  for (const [key, path] of Object.entries(endpoints)) {
    const section = document.getElementById(`${key}Section`);
    try {
      const res = await fetch(`http://127.0.0.1:8000${path}`);
      const data = await res.json();

      section.innerHTML = "";
      if (Array.isArray(data) && data.length > 0) {
        data.forEach((item) => {
          const div = document.createElement("div");
          div.className = "feature-item";
          div.innerText = item.title || item.name || JSON.stringify(item);
          section.appendChild(div);
        });
      } else {
        section.textContent = "No information available";
      }
    } catch (err) {
      section.textContent = "Error loading data";
    }
  }
}

window.addEventListener("DOMContentLoaded", fetchFrontendSections);

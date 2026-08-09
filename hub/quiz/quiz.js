import { lessons, checks } from "../lessons.js";
const mount = document.querySelector("#quiz");
let answers = {};
function render(show = false) {
  const items = lessons.map((lesson, n) => {
    const q = checks[lesson.id]; const picked = answers[lesson.id];
    return `<article class="quiz-card"><p class="eyebrow">${lesson.level.toUpperCase()} · ${lesson.title}</p><h2>${n + 1}. ${q.question}</h2>${q.choices.map((choice, i) => `<label class="quiz-choice ${show ? (i === q.answer ? "correct" : picked === i ? "incorrect" : "") : ""}"><input type="radio" name="${lesson.id}" value="${i}" ${picked === i ? "checked" : ""}> ${choice}</label>`).join("")}${show ? `<p class="feedback">${picked === q.answer ? "Correct. " : "Review this: "}${q.explanation}</p>` : ""}</article>`;
  }).join("");
  const score = show ? `<div class="score"><h2>${Object.entries(checks).filter(([id,q]) => answers[id] === q.answer).length} / ${lessons.length}</h2><p>Use the explanations to revisit the related lesson in the Hub.</p><a class="button" href="../">Return to the Learning Hub ↗</a></div>` : "";
  mount.innerHTML = `${items}<button class="button" id="grade">Grade my knowledge check</button>${score}`;
  mount.querySelectorAll("input").forEach(input => input.onchange = () => { answers[input.name] = Number(input.value); });
  mount.querySelector("#grade").onclick = () => render(true);
}
render();

const note = document.getElementById("note");

note.value = localStorage.getItem("note") || "";

note.onchange = (e) => {
  localStorage.setItem("note", e.target.value);
};

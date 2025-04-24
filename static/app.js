// JS to handle API calls
let token = ""

async function register() {
  const res = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: document.getElementById("username").value,
      password: document.getElementById("password").value,
    }),
  })
  // OLD WAY, 2 STEP REGISTER
  // if (res.ok) {
  //   alert("Registered! Now log in.")
  // } else {
  //   alert("Registration failed.")
  // }
  const data = await res.json()
  if (data.access_token) {
    token = data.access_token
    document.getElementById("auth-section").style.display = "none"
    document.getElementById("task-section").style.display = "block"
    loadTasks()
  } else {
    alert("Registration failed.")
  }
}

async function login() {
  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: document.getElementById("username").value,
      password: document.getElementById("password").value,
    }),
  })
  const data = await res.json()
  if (data.access_token) {
    token = data.access_token
    document.getElementById("auth-section").style.display = "none"
    document.getElementById("task-section").style.display = "block"
    loadTasks()
  } else {
    alert("Login failed.")
  }
}

async function loadTasks() {
  const res = await fetch("/tasks/", {
    headers: { Authorization: `Bearer ${token}` },
  })
  const tasks = await res.json()
  const list = document.getElementById("task-list")
  list.innerHTML = ""
  tasks.forEach(task => {
    const li = document.createElement("li")
    li.innerHTML = `
      ${task.title} (${task.is_completed ? "✅" : "❌"})
      <button onclick="deleteTask(${task.id})">❌</button>
    `
    list.appendChild(li)
  })
}

async function addTask() {
  const title = document.getElementById("new-title").value
  const description = document.getElementById("new-desc").value
  await fetch("/tasks/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title, description }),
  })
  document.getElementById("new-title").value = ""
  document.getElementById("new-desc").value = ""
  loadTasks()
}

async function deleteTask(id) {
  await fetch(`/tasks/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  })
  loadTasks()
}

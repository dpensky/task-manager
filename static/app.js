// JS to handle API calls
let token = localStorage.getItem("token")

window.onload = () => {
  if (token) {
    document.getElementById("auth-section").style.display = "none"
    document.getElementById("task-section").style.display = "block"
    loadTasks()
  }
}

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
    localStorage.setItem("token", data.access_token)
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
    localStorage.setItem("token", data.access_token)
    token = data.access_token
    document.getElementById("auth-section").style.display = "none"
    document.getElementById("task-section").style.display = "block"
    loadTasks()
  } else {
    alert("Login failed.")
  }
}

// async function loadTasks() {
//   const res = await fetch("/tasks/", {
//     headers: { Authorization: `Bearer ${token}` },
//   })
//   const tasks = await res.json()
//   const list = document.getElementById("task-list")
//   list.innerHTML = ""
//   tasks.forEach(task => {
//     const li = document.createElement("li")
//     li.innerHTML = `
//       ${task.title} (${task.is_completed ? "✅" : "❌"})
//       <button onclick="deleteTask(${task.id})">❌</button>
//     `
//     list.appendChild(li)
//   })
// }

async function loadTasks() {
  const res = await fetch("/tasks", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  const data = await res.json()
  const taskList = document.getElementById("task-list")
  taskList.innerHTML = "" // Clear list before rendering

  data.forEach(task => {
    const li = document.createElement("li")
    // if (task.is_completed) {
    //   li.classList.add("completed")
    // }

    const checkbox = document.createElement("input")
    checkbox.type = "checkbox"
    checkbox.checked = task.is_completed
    checkbox.onchange = () => toggleTask(task.id, !task.is_completed)

    const span = document.createElement("span")
    span.textContent = task.title
    if (task.is_completed) {
      span.classList.add("completed")
    }
    const deleteBtn = document.createElement("button")
    deleteBtn.textContent = "🗑️"
    deleteBtn.className = "btn"
    deleteBtn.style.marginLeft = "auto"
    deleteBtn.style.background = "#f87171"
    deleteBtn.style.color = "white"
    deleteBtn.onclick = () => deleteTask(task.id)

    li.appendChild(checkbox)
    li.appendChild(span)
    li.appendChild(deleteBtn)
    taskList.appendChild(li)
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

function logout() {
  localStorage.removeItem("token")
  token = null
  document.getElementById("auth-section").style.display = "block"
  document.getElementById("task-section").style.display = "none"
}

async function toggleTask(id, is_completed) {
  await fetch(`/tasks/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ is_completed }),
  })

  loadTasks() // Refresh the list after updating
}

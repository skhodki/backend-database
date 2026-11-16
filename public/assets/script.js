/**
 * public/assets/scripts.js
 */


let allUsers = []
const users = document.getElementById("users")
const user = document.getElementById("user")


fetch("/users")
.then(response => response.json())
.then(showUsers)


function showUsers(userArray) {
  allUsers = userArray
  console.log("users", JSON.stringify(users, null, '  '));
  while(users.firstChild) {
    users.removeChild(users.lastChild)
  }

  userArray.forEach(user => {
    // {
    //   "username": "Anya",
    //   "email": "anya@example.com",
    //   "city": "Moscow"
    // }

    const { username } = user
    const option = document.createElement("option")
    option.value = username
    option.textContent = username
    users.append(option)
  })

  // const option = document.createElement("option")
  // option.value = "__add"
  // option.textContent = "Add User..."
  // users.append(option)

  setUser({ target: { value: userArray[0].username }})
}


users.addEventListener("change", setUser)


function setUser({ target }) {
  const { value } = target
  if (value === "__add") {
    // TODO: Show Add User UI
    return
  }

  const userData = allUsers.find(({ username }) => (
    username === value
  ))
  user.textContent = JSON.stringify(userData, null, '  ')
  
}
const API_URL = "/api/employees";

const employeeForm = document.getElementById("employee-form");
const employeeTableBody = document.getElementById(
  "employee-table-body"
);
const messageElement = document.getElementById("message");
const refreshButton = document.getElementById("refresh-button");

async function loadEmployees() {
  employeeTableBody.innerHTML = `
    <tr>
      <td colspan="5">Loading employees...</td>
    </tr>
  `;

  try {
    const response = await fetch(API_URL);

    if (!response.ok) {
      throw new Error("Unable to retrieve employees");
    }

    const employees = await response.json();

    employeeTableBody.innerHTML = "";

    if (employees.length === 0) {
      employeeTableBody.innerHTML = `
        <tr>
          <td colspan="5">No employees found</td>
        </tr>
      `;

      return;
    }

    employees.forEach((employee) => {
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${employee.id}</td>
        <td>${employee.name}</td>
        <td>${employee.email}</td>
        <td>${employee.department}</td>
        <td>
          <button
            class="delete-button"
            onclick="deleteEmployee(${employee.id})"
          >
            Delete
          </button>
        </td>
      `;

      employeeTableBody.appendChild(row);
    });
  } catch (error) {
    employeeTableBody.innerHTML = `
      <tr>
        <td colspan="5">${error.message}</td>
      </tr>
    `;
  }
}

employeeForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const department = document
    .getElementById("department")
    .value
    .trim();

  try {
    const response = await fetch(API_URL, {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        name,
        email,
        department
      })
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Unable to add employee");
    }

    showMessage("Employee added successfully", "success");

    employeeForm.reset();

    await loadEmployees();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

async function deleteEmployee(employeeId) {
  const confirmed = window.confirm(
    "Are you sure you want to delete this employee?"
  );

  if (!confirmed) {
    return;
  }

  try {
    const response = await fetch(`${API_URL}/${employeeId}`, {
      method: "DELETE"
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Unable to delete employee");
    }

    showMessage("Employee deleted successfully", "success");

    await loadEmployees();
  } catch (error) {
    showMessage(error.message, "error");
  }
}

function showMessage(message, type) {
  messageElement.textContent = message;
  messageElement.className = type;

  setTimeout(() => {
    messageElement.textContent = "";
    messageElement.className = "";
  }, 4000);
}

refreshButton.addEventListener("click", loadEmployees);

loadEmployees();
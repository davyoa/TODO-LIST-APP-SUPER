<template>
  <div class="container-sm mt-5">
    <h1 class="text-body-secondary">TODOS</h1>

    <div class="input-group mb-3 center">
      <span class="input-group-text" id="basic-addon1">New Todo</span>
      <input type="text" id="new_todo" class="form-control" placeholder="Add New Todo" aria-describedby="basic-addon1"/>
      <button class="btn btn-primary" @click="addTodo()">Add</button>
    </div>

    <div class="list-group">
      <!-- List Group Starts Here -->
      <div v-for="todo in todos" :key="todo.id" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center gap-3">
        <div class="form-check " style="width: 100%;">
          <input class="form-check-input" @click="markDone(todo.id, !todo.done)" type="checkbox" value="" :checked="todo.done" />
          <span v-if="todoKey !== todo.id">{{ todo.text }}</span>
          <input type="text" :value="todo.text" v-if="todoKey === todo.id" id="update_todo" class="form-control " placeholder="Add New Todo" aria-describedby="basic-addon1"/>
        </div>
        
        <div class="d-flex gap-2">
          <!-- Conditional Rendering of Buttons Based on Edit State -->
          <button class="btn btn-success" @click="updateTodo(todo.id)" v-if="todoKey === todo.id">Update</button>

          <button class="btn btn-success" @click="startEdit(todo.id)" v-if="todoKey !== todo.id">Edit</button>
          <button class="btn btn-danger" @click="deleteTodo(todo.id)" v-if="todoKey !== todo.id">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  const todos = ref([]);
  const update = ref(false);
  const todoKey = ref(null);

  useHead({
    link: [{
      rel: "stylesheet",
      href: "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css",
      integrity: "sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB",
      crossorigin: "anonymous"
    }],

    head: [{
      rel: "script",
      src: "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js",
      integrity: "sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI",
      crossorigin: "anonymous"
    }]
  })

  // Full Crud Ops
  onMounted(async ()=>{
    const res = await $fetch('http://127.0.0.1:8000/todos');
    console.log(res);
    todos.value = res;
  })

  const addTodo = async () => {
    const newTodoInput = document.getElementById('new_todo');
    const newTodoText = newTodoInput.value.trim();
    if (newTodoText) {
      const res = await $fetch('http://127.0.0.1:8000/todos', {
        method: 'POST',
        body: { text: newTodoText }
      });

      todos.value.push(res);
      newTodoInput.value = ''; // Clear the Input Field
    }
  }

  const updateTodo = async (id) => {
    const updateInput = document.getElementById('update_todo');
    const text = updateInput.value.trim();
    if (!text) return; // Do not update if text is empty

    const res = await $fetch(`http://127.0.0.1:8000/todos/${id}`, {
      method: 'PUT',
      body: { text: text }
    });

    todos.value = todos.value.map(todo => 
      todo.id === id ? res : todo
    );

    updateInput.value = ''; // Clear the Input Field

    update.value = false;
    todoKey.value = null;
  }

  const deleteTodo = async (id) => {
    try {
      const res = await $fetch(`http://127.0.0.1:8000/todos/${id}`, {
        method: 'DELETE'
      });

      if (res.message === "Todo deleted") {
        todos.value = todos.value.filter(todo => todo.id !== id);
      }
    } catch (err) {
      console.error("Failed to delete todo:", err);
    }
  }


  const markDone = async (id, done) => {
    const res = await $fetch(`http://127.0.0.1:8000/todos/${id}`, {
      method: 'PUT',
      body: { done: done }
    });
  }

  const startEdit = (id) => {
    update.value = true;
    todoKey.value = id;
  }

  
</script>

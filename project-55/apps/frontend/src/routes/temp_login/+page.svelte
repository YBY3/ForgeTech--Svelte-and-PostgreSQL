<script>
    let username = "";
    let email = "";
    let password = "";
    let message = "";
  
    async function handleSignup() {
  const response = await fetch("http://localhost:5000/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password })
  });
  
      const result = await response.json();
      if (!response.ok) {
        message = "Error: " + result.message;
      } else {
        message = result.message;
        // Clear the form after successful signup
        username = "";
        email = "";
        password = "";
      }
    }
  </script>
  
  <form on:submit|preventDefault={handleSignup}>
    <input type="text" bind:value={username} placeholder="Username" required />
    <input type="email" bind:value={email} placeholder="Email" required />
    <input type="password" bind:value={password} placeholder="Password" required />
    <button type="submit">Sign Up</button>
  </form>
  
  <p>{message}</p>
  
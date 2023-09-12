document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');
  
    signupForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const sname = document.getElementById('sname').value;
      const sstud_id = document.getElementById('sstud_id').value;
      const spassword = document.getElementById('spassword').value;
  
      // Perform client-side validation here if needed
      if(sstud_id > 1000000)
      {
        signupForm.reset();
        alert("Student ID cannot exceed 6 digits !");
        return;
      }
    
  
      const data = {
        sname: sname,
        sstud_id: sstud_id,
        spassword: spassword,
      };
  
      // Send a POST request to your Flask server
      fetch('/signup', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if(data.success)
          {
            alert("Registration Successful ! Please login !");
            signupForm.reset();
          }
          if(!data.success)
          {
            alert("Student ID already exists!");
            signupForm.reset();
          }
          console.log(data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    });
  
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const loginStudId = document.getElementById('lstud_id').value;
      const loginPassword = document.getElementById('lpassword').value;
  
      // Perform client-side validation here if needed
  
      const data = {
        lstud_id: loginStudId,
        lpassword: loginPassword,
      };
  
      // Send a POST request to your Flask server
      fetch('/login', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((response) => response.json())
        .then((data) => {
          // Handle the response from the server (data) here
          const adminvalue=data.admin;
          if(data.success)
          { 
            if(adminvalue === 1)
            {
              alert("Welcome Admin");
              loginForm.reset();
              setTimeout(function(){
                  window.location.href="/admin-panel";
              }, 1000);
            }
            else
            {
              alert("Login Successful");
              loginForm.reset();
              setTimeout(function(){
                  window.location.href="/home";
              }, 1000);
            }
          }
          if(!data.success)
          {
            alert("Invalid Username or Password");
            loginForm.reset();
          }
          console.log(data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    });
  });
  
async function checkAuth() {
            try {
                const res = await fetch('/users/me');
                if (res.status === 401) {
                    window.location.href = '/auth/google';
                    return;
                }
                const user = await res.json();
                
                document.getElementById('name').innerText = user.full_name || "User";
                document.getElementById('email').innerText = user.email;
                if (user.profile_picture) {
                    document.getElementById('avatar').src = user.profile_picture;
                }
                
                document.getElementById('loading').style.display = 'none';
                document.getElementById('dashboard').style.display = 'block';
            } catch (err) {
                console.error(err);
            }
        }

       async function initiatePayment() {
            const btn = document.querySelector('button');
            const msg = document.getElementById('msg');
            const input = document.getElementById('amountInput'); 
            
            const nairaAmount = parseFloat(input.value);
            if (!nairaAmount || nairaAmount < 1) {
                msg.innerText = "Please enter a valid amount (Min 1 NGN)";
                return;
            }

            const koboAmount = Math.floor(nairaAmount * 100);

            btn.disabled = true;
            btn.innerText = "Processing...";
            msg.innerText = "";

            try {
                const res = await fetch('/payments/paystack/initiate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ amount: koboAmount }) 
                });

                const data = await res.json();

                if (res.ok) {
                    window.location.href = data.authorization_url;
                } else {
                    msg.innerText = "Error: " + (data.detail || "Payment failed");
                    btn.disabled = false;
                    btn.innerText = "Pay with Paystack";
                }
            } catch (err) {
                msg.innerText = "Network Error";
                btn.disabled = false;
            }
        }

        checkAuth();
import streamlit_authenticator as stauth

# Jo password aap rakhna chahte hain usay yahan likhein
hashed_password = stauth.Hasher(['admin123']).generate()
print(hashed_password)
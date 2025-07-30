import React from "react";
import { GoogleLogin, type CredentialResponse } from '@react-oauth/google';
import { useNavigate } from "react-router-dom";
import { useAuthContext } from "../context/AuthContext.tsx";

const SigninPage: React.FC = () => {
  const authContext = useAuthContext();
  const navigate = useNavigate();

  if (!authContext) {
    throw new Error("AuthContext not found");
  }

  const { setIsGoogleLoggedIn, setHasAccount } = authContext;


  return (
    <section className="w-120 flex flex-col justify-center items-center shadow-md rounded-lg p-4 bg-white dark:bg-gray-800">

			<div className="w-full flex flex-col justify-center items-center mb-4">
				<h2 className="text-2xl font-bold mb-4">Sign in/up</h2>
        <img src="/icon.jpg" alt="World Headlines Logo" className="w-52 h-52" />
      </div>
			<div className="w-full flex justify-center items-center">
				<GoogleLogin
					onSuccess={(response: CredentialResponse)=>{
						console.log("Google Login Success", response);
            setIsGoogleLoggedIn(true);
            setHasAccount(false);
            navigate("/signup");
					}}
					onError={() => {
						console.log("Google Login Failed");
					}}
					size="large"
				/>
			</div>
      
    </section>
  );
};

export default SigninPage;
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthContext } from "../context/AuthContext.tsx";

const SignupPage: React.FC = () => {
  const authContext = useAuthContext();
  const navigate = useNavigate();

  if (!authContext) {
    throw new Error("AuthContext not found");
  }

  const { isGoogleLoggedIn, hasAccount } = authContext;

  useEffect(() => {
    if (!isGoogleLoggedIn) {
      navigate("/signin");
    }
    if (hasAccount) {
      navigate("/");
    }
  }, [isGoogleLoggedIn]);

  if (!isGoogleLoggedIn) {
    return null; // or a loading spinner
  }

  return (
    <section className="w-120 flex flex-col justify-center items-center shadow-md rounded-lg p-4 bg-white dark:bg-gray-800">

			<div className="w-full flex flex-col justify-center items-center mb-4">
				<h2 className="text-2xl font-bold mb-4">Sign up</h2>
        <img src="/icon.jpg" alt="World Headlines Logo" className="w-52 h-52" />
        
      </div>
			<div className="w-full flex justify-center items-center">

			</div>
      
    </section>
  );
};

export default SignupPage;
import React from "react";
import Layout from "../components/Layout";

interface HomePageProps {
  countryCodes: string[];
}

const HomePage: React.FC<HomePageProps> = (props: HomePageProps) => {
  const { countryCodes } = props;

  return (
  <div>
    <h1>Home Page</h1>
  </div>
  )
}
export default HomePage;
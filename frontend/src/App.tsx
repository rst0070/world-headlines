import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import CountryPage from './pages/CountryPage'
import HomePage from './pages/HomePage'
import './App.css'
import Layout from './components/Layout';
import { getCountryCodes } from './services/api.country';
import { useState } from 'react';

async function App() {
  const [countryCodes, setCountryCodes] = useState<string[]>([]);

  setCountryCodes(await getCountryCodes());

  return (
    <Router>
      <Routes>
        <Route path="/" element={
            <Layout countryCodes={countryCodes}>
              <HomePage countryCodes={countryCodes} />
            </Layout>
          }
        />
        <Route path="/country/:countryCode" element={
          <Layout countryCodes={countryCodes}>
            <CountryPage countryCode={countryCodes[0]} />
          </Layout>
        }
      />
      </Routes>
    </Router>
  )
}

export default App

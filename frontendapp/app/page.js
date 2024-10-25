"use client";
import { useState, useEffect } from 'react';
import Image from "next/image";
import Link from 'next/link';
import { initializeApp } from "firebase/app";
//import { getAnalytics } from "firebase/analytics";
import { getFirestore, collection, addDoc } from 'firebase/firestore';

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCRmrJkZsI61AxtEDTyZrZ5w1yksQbh0d0",
  authDomain: "bitbandits-97237.firebaseapp.com",
  projectId: "bitbandits-97237",
  storageBucket: "bitbandits-97237.appspot.com",
  messagingSenderId: "769278793816",
  appId: "1:769278793816:web:958e373b1d128ff9cd922d",
  measurementId: "G-42Q6CY4VXT"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export default function Home() {
  const [formData, setFormData] = useState({
    batterySize: 50,
    maxBatteryPower: 10,
    solarPanelSize: 5,
    averageConsumption: 20,
    solarPanelDirection: 'Sør',
    consumptionPattern: 'Bolig'
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitting data:', formData); // Log the data being submitted
    try {
      await addDoc(collection(db, 'energyData'), formData);
      alert('Data submitted successfully!');
    } catch (error) {
      console.error('Error adding document: ', error);
      alert('Error submitting data. Please try again.');
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-4 sm:p-24 text-white">
      <div className="fixed inset-0 z-0 flex items-center justify-center">
      <img className="object-cover w-3/4 h-auto" src="https://media.giphy.com/media/26BRKEDGBicmow252/giphy.gif"  alt="homegif" />
</div>

      <div className="relative z-10 flex justify-center transform translate-y-8 sm:translate-y-32 h-screen">
        <h1 className="text-6xl sm:text-[20rem] font-bold text-center text-white">
          BitBandits
        </h1>
      </div>

      <div className="relative flex place-items-center z-10 mb-8 sm:mb-0">
        <h1 className="text-3xl sm:text-6xl font-bold mb-10 text-center text-white">
          Optimalizer energien din
        </h1>
      </div>

      <div className="relative flex place-items-center z-10 mb-8 sm:mb-0">
        <Link href="/projects" className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:bg-white/10 hover:border-white/20">
          <h2 className=" max-w-[30ch] text-sm opacity-70 mb-3 sm:text-5xl font-semibold">
            <div className="inline-block ">
              Projects{" "}
            </div>
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-80">
            take a look at what I&apos;ve been building.
          </p>
        </Link>

        <Link href="/resume" className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:bg-white/10 hover:border-white/20">
          <h2 className=" max-w-[30ch] text-sm opacity-70 mb-3 sm:text-5xl font-semibold">
            <div className="inline-block">
              Resume
            </div>
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-80">
            just read the pdf.
          </p>
        </Link>
      </div>

      <div className="w-full flex flex-col sm:flex-row items-center justify-between font-mono text-sm">

        <div className="flex justify-center space-x-4 mb-10">
          <a
            href="https://github.com/adisinghstudent?tab=stars"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center"
          >
            <Image
              src="/githubb.png"
              alt="Github"
              className="invert"
              width={45}
              height={24}
              priority
            />
          </a>
          <a
            href="https://linkedin.com/in/adisinghwork"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center"
          >
            <Image
              src="/linkedin.png"
              alt="Linkedin"
              className="invert"
              width={45}
              height={24}
              priority
            />
          </a>
          </div>
        </div>

      <div className="relative z-10 w-full max-w-6xl mx-auto mt-16 flex flex-col md:flex-row justify-between">
        <form onSubmit={handleSubmit} className="w-full md:w-1/2 space-y-6">
          <div>
            <label htmlFor="batterySize" className="block text-sm font-medium">
              Størrelse på batteri (kWh): {formData.batterySize}
            </label>
            <input
              type="range"
              id="batterySize"
              name="batterySize"
              min="0"
              max="100"
              value={formData.batterySize}
              onChange={handleInputChange}
              className="w-full"
            />
          </div>
          {/* Add similar slider inputs for other parameters */}
          <div>
            <label htmlFor="solarPanelDirection" className="block text-sm font-medium">
              Retning på solcelleanlegget
            </label>
            <select
              id="solarPanelDirection"
              name="solarPanelDirection"
              value={formData.solarPanelDirection}
              onChange={handleInputChange}
              className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-black"
            >
              <option>Sør</option>
              <option>Øst</option>
              <option>Vest</option>
              <option>Nord</option>
            </select>
          </div>
          <div>
            <label htmlFor="consumptionPattern" className="block text-sm font-medium">
              Forbruksmønster
            </label>
            <select
              id="consumptionPattern"
              name="consumptionPattern"
              value={formData.consumptionPattern}
              onChange={handleInputChange}
              className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm text-black"
            >
              <option>Fabrikk</option>
              <option>Næringsbygg</option>
              <option>Bolig</option>
            </select>
          </div>
          <button type="submit" className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Submit
          </button>
        </form>

        <div className="w-full md:w-1/2 mt-8 md:mt-0 md:ml-8 p-6 bg-white/10 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-4">Entered Information</h2>
          <ul className="space-y-2">
            <li>Størrelse på batteri: {formData.batterySize} kWh</li>
            <li>Max effekt på batteri: {formData.maxBatteryPower} kW</li>
            <li>Størrelse på solcelleanlegget: {formData.solarPanelSize} kW</li>
            <li>Gjennomsnittlig forbruk: {formData.averageConsumption} kWh</li>
            <li>Retning på solcelleanlegget: {formData.solarPanelDirection}</li>
            <li>Forbruksmønster: {formData.consumptionPattern}</li>
          </ul>
        </div>
      </div>
    </main>
  );
}


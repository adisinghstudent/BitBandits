"use client";

import Link from 'next/link';
import Image from 'next/image';
import { useRef } from 'react';

const projects = [
  { 
    id: 1, 
    title: "Llama Chat", 
    description: "An innovative chatbot application powered by the Llama model, designed to provide engaging AI-generated conversations. It features a robust Node.js backend for seamless message processing and a user-friendly React Native frontend for intuitive interaction, allowing users to chat and receive instant responses from the AI.", 
    videoSrc: "/llamachat.mov",
    languages: [
      { name: "JavaScript", iconSrc: "/icons/js.png" },
      { name: "React Native", iconSrc: "/icons/react.png" },
      { name: "Node.js", iconSrc: "/icons/node-js.png" }
    ]
  },
  { 
    id: 2, 
    title: "Fremtek.com", 
    description: "A comprehensive full-stack web application developed for a cloud platform operator, offering scalable solutions and efficient management tools. This project showcases advanced features that enhance user experience and streamline operations in a cloud environment.", 
    videoSrc: "/fremtek.mp4",
    languages: [
      { name: "Typescript", iconSrc: "/icons/typescript.png" },
      { name: "Html", iconSrc: "/icons/html.png" },
      { name: "Css", iconSrc: "/icons/css.png" },
      { name: "Firebase", iconSrc: "/icons/database.png" }
    ]
  },
  { 
    id: 3, 
    title: "Snapclass", 
    description: "A dynamic social media platform tailored for students, enabling them to share and showcase their photos during class hours. This web app fosters community engagement and collaboration, making it easy for students to connect and share their experiences visually.", 
    imageSrc: "/SnapClass.png",
    languages: [
      { name: "Javascript", iconSrc: "/icons/js.png" },
      { name: "Python", iconSrc: "/icons/python.png" },
      { name: "Html", iconSrc: "/icons/html.png" },
      { name: "Css", iconSrc: "/icons/css.png" },
      { name: "Firebase", iconSrc: "/icons/database.png" }
    ] // Add languages as needed
  },
];

export default function Projects() {
  const videoRefs = useRef(projects.map(() => null));

  const handleMouseEnter = (index) => {
    if (videoRefs.current[index]) {
      videoRefs.current[index].play();
    }
  };

  const handleMouseLeave = (index) => {
    if (videoRefs.current[index]) {
      videoRefs.current[index].pause();
      videoRefs.current[index].currentTime = 0;
    }
  };

  return (
    <main className="flex flex-col items-center justify-between p-4 sm:p-24 text-white">
      <div className="w-full flex justify-start mb-8">
        <Link href="/" className="text-sm sm:text-3xl font-semibold opacity-70">
          <div className="inline-block">go back home</div>
        </Link>
      </div>

      <h1 className="text-6xl sm:text-[10rem] font-bold mb-12 text-center">Projects</h1>

      <div className="w-full">
        {projects.map((project, index) => (
          <div
            key={project.id}
            className={`flex flex-col sm:flex-row ${index % 2 === 0 ? 'sm:flex-row-reverse' : ''} items-center mb-8`}
            onMouseEnter={() => handleMouseEnter(index)}
            onMouseLeave={() => handleMouseLeave(index)}
          >
            <div className="relative w-full sm:w-1/2 h-64 sm:h-auto">
              {project.videoSrc ? (
                <video
                  ref={el => videoRefs.current[index] = el}
                  src={project.videoSrc}
                  className="absolute inset-0 w-full h-full object-cover rounded-xl"
                  playsInline
                  muted
                  loop
                />
              ) : project.imageSrc ? (
                <Image
                  src={project.imageSrc}
                  alt={project.title}
                  fill
                  className="object-cover rounded-lg"
                />
              ) : (
                <div className="absolute inset-0 flex items-center justify-center bg-gray-200 rounded-lg">
                  <p>No media available</p>
                </div>
              )}
            </div>

            <div className="p-4 sm:w-1/2">
              <h2 className="text-xl sm:text-2xl font-bold mb-2">{project.title}</h2>
              <p className="text-xs">{project.description}</p>
              <div className="mt-4">
                <h3 className="text-lg font-semibold mb-2">Languages Used:</h3>
                <div className="flex flex-wrap">
                  {project.languages.map((language, langIndex) => (
                    <div key={langIndex} className="flex items-center mr-4 mb-2">
                      <img src={language.iconSrc} alt={language.name} className="w-6 h-6 mr-2" />
                      <span className="text-sm">{language.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <Link href="https://www.instagram.com/adisinghbuilds/" className="group rounded-lg border-transparent transition-colors hover:bg-white-800 hover:dark:border-neutral-700 mt-12">
        <h2 className="text-xl sm:text-2xl font-semibold">
          <div className="group-hover:hidden">watch me build</div>
          <div className="hidden group-hover:block">
            <Image src="/Instagram.png" alt="Watch me build" width={110} height={110} />
          </div>
        </h2>
      </Link>
    </main>
  );
}
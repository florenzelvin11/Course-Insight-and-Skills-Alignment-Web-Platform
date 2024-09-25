export function mockServer(method, path, data, error) {
  console.log(`Request: ${method} ${path}`);
  if (data) {
    console.log(`Request Data: `, data);
  }

  if (error) {
    return {
      error: "Fake mock server error.",
    };
  }

  if (path === "/login") {
    return {
      token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
      userType: "academic",
    };
  }

  if (path === "/register") {
    return {
      message: "Successful registration, verify account now.",
    };
  }

  if (path === "/verifyCode" && method === "POST") {
    return {
      token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
      userType: "admin",
    };
  }

  if (path === "/courses/student") {
    return {
      courses: [
        {
          name: "Introduction to Computer Science",
          code: "COMP1111",
          school: "Computer Science Department",
          thumbnail:
            "https://i.natgeofe.com/n/6e8d8a34-243d-4b47-9de2-a393271de8f7/3143130_3x4.jpg",
        },
        {
          name: "Calculus I",
          code: "MATH101",
          school: "Mathematics Department",
          thumbnail:
            "https://upload.wikimedia.org/wikipedia/commons/7/79/2010-brown-bear.jpg",
        },
        {
          name: "History of Art",
          code: "ART200",
          school: "Fine Arts Department",
          thumbnail:
            "https://gifts.worldwildlife.org/gift-center/Images/large-species-photo/large-Grizzly-Bear-photo.jpg",
        },
      ],
    };
  }

  if (path === "/courses/academic") {
    return {
      courses: [
        {
          name: "Introduction to Computer Science",
          code: "COMP1111",
          school: "Computer Science Department",
          thumbnail:
            "https://i.natgeofe.com/n/6e8d8a34-243d-4b47-9de2-a393271de8f7/3143130_3x4.jpg",
        },
        {
          name: "History of Art",
          code: "ART200",
          school: "Fine Arts Department",
          thumbnail:
            "https://gifts.worldwildlife.org/gift-center/Images/large-species-photo/large-Grizzly-Bear-photo.jpg",
        },
      ],
    };
  }

  if (path.startsWith("/courses/") && method === "PUT") {
    return {
      message: "Course updated successfully",
    };
  }

  if (path.startsWith("/courses/") && method === "GET") {
    return {
      name: "Computer Science Project",
      code: "COMP3900",
      uoc: 12,
      topics: [
        "Fundamental programming concepts",
        "Introduction to Computer Science",
      ],
      description:
        "An introductory course covering the basics of computer science and programming.",
      skills: {
        "Swift" : 20,
        "Angular" : 30.44,
        "Python" : 50
      },
      knowledge: {
        "c++" : 20,
        "Java" : 30,
        "data structures" : 50
      },
      thumbnail:
            "https://i.natgeofe.com/n/6e8d8a34-243d-4b47-9de2-a393271de8f7/3143130_3x4.jpg",
      currentVersion: "1",
      school: "Computer Science School",
      availableVersions: ["1", "2"],
      currentYear: 2022,
      currentTerm: "T2",
      availableYearTerms: [
        [2022, "T2"],
        [2023, "T3"],
      ],
    };
  }

  if (path === "/logout") {
    return {
      message: "logged out",
    };
  }

  if (path === "/projects/academic" || path === "/projects/student") {
    return {
      projects: [
        {
          id: 1,
          name: "Fitness Tracker",
          knowledge: { "JavaScript": 90, "React": 10 },
          skills: { "writing": 60, "speaking": 40 },
          client: "Jane Doe",
          thumbnail:
            "https://cdn.dribbble.com/users/1233499/screenshots/4571542/photoshop1.gif",
        },
        {
          id: 2,
          name: "Recipe App",
          knowledge: { "Python": 90, "Django": 10 },
          skills: { "writing": 60, "speaking": 40 },
          client: "Alice Johnson",
          thumbnail:
            "https://techcrunch.com/wp-content/uploads/2022/01/Multi-Device.jpg",
        },
        {
          id: 3,
          name: "E-commerce Website",
          knowledge: { "JavaScript" : 60, "Vue.js" : 30, "Firebase": 10 },
          skills: { "writing": 60, "speaking": 40 },
          client: "Bob Williams",
          thumbnail: "https://colorlib.com/wp/wp-content/uploads/sites/2/ecommerce-website-builder.jpg",
        },
      ],
    };
  }

  if (path.startsWith("/projects/") && method === "GET") {
    return {
      id: 1,
      name: "Fitness Tracker",
      client: "Jane Doe",
      skills: { "JavaScript": 90, "React": 10 },
      knowledge: { "writing": 60, "speaking": 40 },
      thumbnail:  "https://cdn.dribbble.com/users/1233499/screenshots/4571542/photoshop1.gif",
      scope: "The scope of the fitness tracker programming project includes developing a comprehensive application that can accurately track and record user’s physical activities such as steps taken, distance covered, calories burned, and heart rate. The project will also incorporate features for setting personal fitness goals, monitoring progress over time, and providing health insights based on the collected data. Additionally, the application will ensure user-friendly interfaces, seamless synchronization with various devices, and strict adherence to data privacy and security standards.",
      topics: ["topic 1", "topic 2"],
      percentageMatch: 50,
      missingKnowledge: ["c++", "JavaScript"],
      missingSkills: ["problem solving", "communication"],
      requirements: "Completed COMP1511",
      outcomes: "The fitness tracker programming project aims to develop a comprehensive application that accurately tracks and records users’ physical activities such as steps taken, distance covered, calories burned, and heart rate. It will incorporate features for setting personal fitness goals, monitoring progress over time, and providing health insights based on the collected data, all within a user-friendly interface. The application will also ensure seamless synchronization with various devices and strict adherence to data privacy and security standards. Upon completion, we anticipate increased user engagement, improved health outcomes, demonstrated commitment to data security, successful interoperability with various devices, and high user satisfaction. These outcomes will not only signify the project’s technical success but also its positive impact on users’ fitness journeys, thereby informing future developments and innovations.",
      groups: [
        {
          id: 15,
          groupName: "best group",
          members: ["z5255135", "z5288212"]
        },
        {
          id: 72,
          groupName: "another group",
          members: ["z5455335", "z5282674"]
        }
      ],
    }
  }

  if (path.startsWith("/projects") && method === "POST") {
    return {
      message: "Project updated successfully",
    };
  }
  if (path.startsWith("/projects/join/") && method === "PUT") {
    return {
      message: "User joined group",
    };
  }

  if (path.startsWith("/projects/groupCreate/") && method === "POST") {
    return {
      message: "Created group",
    };
  }

  if (path === '/user/profile' && method === 'GET') {
    return {
      zId: 'z52551351',
      firstName: 'James',
      lastName: 'Adam',
      email: 'z5255135@unsw.edu.au',
      headline: 'Headline string',
      summary: 'summary',
      profilePath:   "https://i.natgeofe.com/n/6e8d8a34-243d-4b47-9de2-a393271de8f7/3143130_3x4.jpg",
      userType: 'admin'
    }
  }
}

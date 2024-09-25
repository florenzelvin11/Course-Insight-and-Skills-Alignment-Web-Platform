import * as React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { Outlet } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import ProfilePage from './pages/ProfilePage';
import ProfileCoursePage from './pages/ProfileCoursePage';
import SettingsPage from './pages/SettingsPage';
import './App.css';
import CourseDashboardPage from './pages/CourseDashboardPage';
import CoursePage from './pages/CoursePage';
import VerificationCodePage from './pages/VerificationCodePage';
import EditCoursePage from './pages/EditCoursePage';
import AddCoursePage from './pages/AddCoursePage';
import { GlobalReloadProvider } from './components/GlobalReloadProvider';
import { CssBaseline, ThemeProvider } from '@mui/material';
import theme from "./theme";
import SimilarStudentsPage from './pages/SimilarStudentsPage';
import PublicProfilePage from './pages/PublicProfilePage';
import AddCourseMenuPage from './pages/AddCourseMenuPage';
import AddCourseUrlPage from './pages/AddCourseUrlPage';
import AddCoursePdfPage from './pages/AddCoursePdfPage';
import ProjectDashboardPage from './pages/ProjectDashboardPage';
import ProjectPage from './pages/ProjectPage';
import AddProjectPage from './pages/AddProjectPage';
import AdminPage from './pages/AdminPage';
import AdminActiveUsers from './components/AdminActiveUsers';
import AdminCourses from './components/AdminCourses';
import AdminProjects from './components/AdminProjects';
import AdminProfileSecurityPage from './pages/AdminProfileSecurityPage';
import AdminDashboard from './components/AdminDashboard';
import ProfileProjectPage from './pages/ProfileProjectPage';

function App() {
  const router = createBrowserRouter([
    { path: '/', element: <LoginPage/> },
    { path: '/signup', element: <SignUpPage/> },
    { path: '/course-dashboard', element: <CourseDashboardPage/> },
    { path: '/course/:courseCode', element: <CoursePage/> },
    { path: '/course/:courseCode/:yearTerm', element: <CoursePage/> },
    { path: '/course/:courseCode/:yearTerm/:version', element: <CoursePage/> },
    { path: '/course-edit/:courseCode', element: <EditCoursePage/> },
    { path: '/course-dashboard', element: <CourseDashboardPage/> },
    { path: '/add-course-menu', element: <AddCourseMenuPage/> },
    { path: '/add-course-url', element: <AddCourseUrlPage/> },
    { path: '/add-course-pdf', element: <AddCoursePdfPage/> },
    { path: '/add-course', element: <AddCoursePage/> },
    { path: '/project-dashboard', element: <ProjectDashboardPage/> },
    { path: '/project/:projectId', element: <ProjectPage/> },
    { path: '/add-project', element: <AddProjectPage/> },
    { path: '/verify-account', element: <VerificationCodePage/> },
    { path: '/verify-account/:zId/:code', element: <VerificationCodePage/> },
    { path: '/profile', element: <ProfilePage />},
    { path: '/profile/:userType/:zID', element: <PublicProfilePage />}, 
    { path: '/profile/:userType/:zID/courses', element: <ProfileCoursePage />},  
    { path: '/profile/student/:zID/projects', element: <ProfileProjectPage />},  
    { path: '/similar-students', element: <SimilarStudentsPage />},  
    { path: '/settings', element: <SettingsPage />},
    { path: '/settings/account-preference', element: <SettingsPage />},
    { path: '/settings/sign-in-and-security', element: <SettingsPage />},
    { path: '/settings/admin/set-user-type', element: <SettingsPage />},
    { path: '/admin', element: <AdminPage content={<AdminDashboard />}/>},
    { path: '/admin/dashboard', element: <AdminPage content={<AdminDashboard />} />},
    { path: '/admin/people', element: <AdminPage content={<AdminActiveUsers />}/>},
    { path: '/admin/courses', element: <AdminPage content={<AdminCourses />}/>},
    { path: '/admin/projects', element: <AdminPage content={<AdminProjects />}/>},
    { path: '/admin/profile/sign-in-and-security/:zID', element: <AdminProfileSecurityPage/>},
  ])



  return (
    <>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <GlobalReloadProvider>
          <RouterProvider router={router}/>
          <Outlet/>
        </GlobalReloadProvider>
      </ThemeProvider>
    </>
  );
}

export default App;

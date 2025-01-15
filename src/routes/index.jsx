import { createHashRouter } from "react-router-dom"; // Use createHashRouter
import AppLayout from "../components/layout/AppLayout";
import LoginPage from "../pages/LoginPage";
import MainLayout from "../components/layout/MainLayout";
import DashboardPage from "../pages/DashboardPage";
import SearchPage from "../pages/SearchPage";
import LandingPage from "../pages/LandingPage";
import SimpleDashBoardPage from "../pages/SimpleDashBoardPage";
import ConnectAccountPage from "../pages/ConnectAccountPage";
import InitialScreen from "../pages/InitialScreen";
import TestPage from '../pages/TestPage'; // Adjust the path if necessary
import CheckoutSuccess from "../pages/CheckoutSuccess";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import PrivacyPolicy from "../pages/PrivacyPolicy";

export const router = createHashRouter([ // Use createHashRouter
  {
    path: "/",
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <LandingPage />
      },
      {
        path: "home",
        element: <AppLayout />,
        children: [
          {
            index: true,
            element: <LandingPage />
          },
        ]
      },
      {
        path: "privacy",
        element: <PrivacyPolicy />,
        children: [
          {
            index: true,
            element: <PrivacyPolicy />
          },
        ]
      },
      {
        path: "dashboard",
        element: <MainLayout />,
        children: [
          {
            index: true,
            element: <SimpleDashBoardPage />
          },
        ]
      },
      {
        path: "about",
        element: <MainLayout />,
        children: [
          {
            index: true,
            element: <InitialScreen />
          },
        ]
      },
      {
        path: "connectAccount",
        element: <MainLayout />,
        children: [
          {
            index: true,
            element: <ConnectAccountPage />
          },
        ]
      },
      {
        path: "search",
        element: <MainLayout />,
        children: [
          {
            index: true,
            element: <SearchPage />
          }
        ]
      },
      {
        path: "test-page",
        element: <MainLayout />,
        children: [
          {
            index: true,
            element: <TestPage />
          }
        ]
      },
      {
        path: "checkout-success",
        children: [
          {
            index: true,
            element: <CheckoutSuccess />
          }
        ]
      }
    ]
  }
]);

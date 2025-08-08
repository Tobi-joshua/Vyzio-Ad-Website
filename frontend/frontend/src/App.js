import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import { Toaster } from "sonner";
import { useEffect, useState } from 'react';
import { Box, Toolbar } from '@mui/material';

// Pages
import Homepage from "./pages/Homepage";
// import SearchResults from "./pages/SearchResults";
// import AdDetails from "./pages/AdDetails";
// import PostAd from "./pages/PostAd";
// import EditAd from "./pages/EditAd";
// import Dashboard from "./pages/Dashboard";
// import Profile from "./pages/Profile";
// import Login from "./pages/Login";
// import Signup from "./pages/Signup";
// import Favorites from "./pages/Favorites";
// import Chat from "./pages/Chat";
// import CategoryListing from "./pages/CategoryListing";
// import AdminPanel from "./pages/AdminPanel";
// import StaticPage from "./pages/StaticPage";
import NotFoundPage from "./NotFound"; 

// Components
import Footer from "./components/Footer";

function App() {

  const [screenWidth, setScreenWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setScreenWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);


  return (
    <>
      <BrowserRouter>
      <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        background: `linear-gradient(to bottom, #f0f0f0, #ffffff)`,
        overflowX: 'hidden',
      }}
    >
    
     <Toolbar sx={{ minHeight: { xs: 56, sm: 64, md: 64 } }} />
          <Routes>
            <Route path="/" element={<Homepage />} />
            {/* Uncomment and add your routes here */}
            {/* <Route path="/search" element={<SearchResults />} /> */}
            {/* <Route path="/ads/:adId" element={<AdDetails />} /> */}
            {/* <Route path="/post-ad" element={<PostAd />} /> */}
            {/* <Route path="/edit-ad/:adId" element={<EditAd />} /> */}
            {/* <Route path="/dashboard" element={<Dashboard />} /> */}
            {/* <Route path="/profile" element={<Profile />} /> */}
            {/* <Route path="/login" element={<Login />} /> */}
            {/* <Route path="/signup" element={<Signup />} /> */}
            {/* <Route path="/favorites" element={<Favorites />} /> */}
            {/* <Route path="/chat" element={<Chat />} /> */}
            {/* <Route path="/categories/:categoryId" element={<CategoryListing />} /> */}
            {/* <Route path="/admin" element={<AdminPanel />} /> */}
            {/* <Route path="/:staticPage" element={<StaticPage />} /> */}

            {/* Fallback route for unmatched URLs */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Box>
        <Footer />
      </BrowserRouter>

      {/* Global Toaster */}
      <Toaster position="top-right" richColors />
    </>
  );
}

export default App;
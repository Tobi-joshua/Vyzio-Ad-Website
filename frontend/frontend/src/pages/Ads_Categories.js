import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  CircularProgress,
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  CardActions,
  Avatar,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import CategoryIcon from "@mui/icons-material/Category";
import { useNavigate } from "react-router-dom";
import VyzionHomePageAppBar from "../components/ResponsiveAppBar";
import DataLoader from "../components/DataLoader";

// Helper to map icon names from backend to MUI icons
import HandymanIcon from '@mui/icons-material/Handyman';
import HomeIcon from '@mui/icons-material/Home';
import WorkIcon from '@mui/icons-material/Work';
import SchoolIcon from '@mui/icons-material/School';
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar';
import DevicesIcon from '@mui/icons-material/Devices';
import StyleIcon from '@mui/icons-material/Style';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import PetsIcon from '@mui/icons-material/Pets';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import GrassIcon from '@mui/icons-material/Grass';
import SportsSoccerIcon from '@mui/icons-material/SportsSoccer';
import ChildCareIcon from '@mui/icons-material/ChildCare';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import FlightTakeoffIcon from '@mui/icons-material/FlightTakeoff';
import PaletteIcon from '@mui/icons-material/Palette';
import SmartphoneIcon from '@mui/icons-material/Smartphone';
import EventIcon from '@mui/icons-material/Event';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import CleaningServicesIcon from '@mui/icons-material/CleaningServices';
import { API_BASE_URL } from "../constants";

// Map backend icon string to MUI icon component
const iconMap = {
  handyman: HandymanIcon,
  home: HomeIcon,
  work: WorkIcon,
  school: SchoolIcon,
  directions_car: DirectionsCarIcon,
  devices: DevicesIcon,
  style: StyleIcon,
  health_and_safety: HealthAndSafetyIcon,
  pets: PetsIcon,
  more_horiz: MoreHorizIcon,
  grass: GrassIcon,
  sports_soccer: SportsSoccerIcon,
  child_care: ChildCareIcon,
  restaurant: RestaurantIcon,
  flight_takeoff: FlightTakeoffIcon,
  palette: PaletteIcon,
  smartphone: SmartphoneIcon,
  event: EventIcon,
  account_balance: AccountBalanceIcon,
  cleaning_services: CleaningServicesIcon,
};

export default function AdsCategories() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  const theme = useTheme();
  const isSmDown = useMediaQuery(theme.breakpoints.down("sm"));
  const navigate = useNavigate();

  // Fetch categories on mount
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/categories/`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch categories");
        return res.json();
      })
      .then((data) => {
        setCategories(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <DataLoader visible={true} />;

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
      <VyzionHomePageAppBar />

      <Typography variant="h4" fontWeight="bold" gutterBottom mt={3}>
      Ads  Categories
      </Typography>

      <Grid container spacing={3}>
        {categories.map(({ id, name, icon }) => {
          const IconComponent = iconMap[icon] || CategoryIcon;
          return (
            <Grid
              item
              key={id}
              xs={12}
              sm={6}
              md={4}
              onClick={() => navigate(`${API_BASE_URL}/categories/${id}/ads`)}
              sx={{ cursor: "pointer" }}
            >
              <Card
                variant="outlined"
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  p: 3,
                  height: "100%",
                  transition: "transform 0.2s",
                  "&:hover": { boxShadow: 6, transform: "scale(1.03)" },
                }}
              >
                <Avatar
                  sx={{
                    bgcolor: theme.palette.primary.main,
                    width: 56,
                    height: 56,
                    mb: 2,
                  }}
                >
                  <IconComponent fontSize="large" />
                </Avatar>
                <CardContent>
                  <Typography
                    variant="h6"
                    component="div"
                    align="center"
                    fontWeight={600}
                  >
                    {name}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`${API_BASE_URL}/categories/${id}/ads`);
                    }}
                    variant="contained"
                    fullWidth
                  >
                    View Ads
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          );
        })}
      </Grid>
    </Container>
  );
}

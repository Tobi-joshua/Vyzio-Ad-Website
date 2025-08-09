// src/screens/Ads_Details.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardMedia,
  Avatar,
  Grid,
  CircularProgress,
} from "@mui/material";
import { API_BASE_URL } from "../constants";

const Ads_Details = () => {
  const { id } = useParams();
  const [ad, setAd] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/ads/${id}/`)
      .then((res) => res.json())
      .then((data) => {
        setAd(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching ad:", err);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={5}>
        <CircularProgress />
      </Box>
    );
  }

  if (!ad) {
    return (
      <Typography color="error" align="center" mt={5}>
        Ad not found.
      </Typography>
    );
  }

  return (
    <Box maxWidth="lg" mx="auto" p={2}>
      {/* Header Image */}
      <Card sx={{ mb: 2 }}>
        <CardMedia
          component="img"
          height="450"
          image={
            ad.header_image
              ? `${API_BASE_URL}${ad.header_image_url}`
              : "https://via.placeholder.com/900x450?text=No+Image"
          }
          alt={ad.title}
        />
      </Card>

      {/* Extra Images Thumbnails */}
      {ad.images?.length > 0 && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          {ad.images.map((img) => (
            <Grid item xs={6} sm={4} md={3} key={img.id}>
              <Card>
                <CardMedia
                  component="img"
                  height="150"
                  image={`${img.image_url}`}
                  alt="Ad Extra"
                />
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Grid container spacing={3}>
        {/* Left: Description & Details */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h5" fontWeight="bold" gutterBottom>
                {ad.title}
              </Typography>
              <Typography variant="h6" color="primary" gutterBottom>
                {ad.currency} {ad.price}
              </Typography>
              <Typography variant="body1" gutterBottom>
                {ad.description}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                📍 {ad.city}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                📅 {new Date(ad.created_at).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Right: Seller Info */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar
                  src={ad.user?.avatar_url || ""}
                  alt={ad.user?.name || "Seller"}
                  sx={{ width: 60, height: 60, mr: 2 }}
                />
                <Typography variant="body1">
                  {ad.user?.name || "Unknown Seller"}
                </Typography>
              </Box>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                onClick={() => alert("Contact seller functionality here")}
              >
                Contact Seller
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Ads_Details;

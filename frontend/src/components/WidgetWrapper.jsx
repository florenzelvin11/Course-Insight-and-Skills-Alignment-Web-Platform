import { Box } from "@mui/material";
import { styled } from "@mui/system";

const WidgetWrapper = styled(Box)(() => ({
  padding: "1.5rem 1.5rem 0.75rem 1.5rem",
  backgroundColor: "#FAFAF5",
  borderRadius: "0.75rem",
  boxShadow: "0px 0px 10px rgba(0, 0, 0, 0.3)", /* Set shadow properties */
  // outline: "2px solid black"
}));

export default WidgetWrapper;

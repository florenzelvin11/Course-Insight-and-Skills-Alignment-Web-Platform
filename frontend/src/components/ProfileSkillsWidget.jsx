import React from 'react';
import Typography from '@mui/material/Typography';
import { BarChart } from '@mui/x-charts/BarChart';
import WidgetWrapper from './WidgetWrapper';
import { Divider, Box, useMediaQuery } from '@mui/material';
import { useGlobalState } from '../components/GlobalReloadProvider';
import { apiCall } from '../helpers/helper';
import LoadingWidget from './LoadingWidget';

const colours = [
  "#BD94E0",
  "#E094BD",
  "#94E094",
  "#E094E0",
  "#94BDE0",
  "#E0BD94",
  "#5A6B04",
  "#E06B5A",
  "#1F2B0E",
  "#E02B1F",
  "#FFA500",
  "#7C1C1C",
  "#1C7C3E",
  "#1C3E7C",
  "#3E1C7C",
  "#7C3E1C",
  "#4D4D4D",
  "#7C1C5B",
  "#5B7C1C",
  "#1C5B7C",
  "#7C5B1C",
  "#5B1C7C",
  "#FF5733",
  "#33FF57",
  "#5733FF",
  "#FF33E9",
  "#E9FF33",
  "#33E9FF",
  "#FF33A8",
  "#A8FF33"
];

const ProfileSkillsWidget = (props) => {
  const isNonMobileScreen = useMediaQuery("(min-width: 1000px)");

  const { globalReload } = useGlobalState()

  const [ isLoading, setIsLoading ] = React.useState(true)
  const [ skillData, setSkillData ] = React.useState(null);

  React.useEffect(() => {
    async function getData() {
      try {
        const response = await apiCall('GET', `/${props.userType}/profile/skills?zID=${props.zID}`)
        // const response = {}
        if (!response.error) {
          setSkillData(response.skills)
          setIsLoading(false)
        }
        return response
      } catch(e) {
        //
      }
    }
    getData()
  }, [globalReload])

  const valueFormatter = (value) => `${value}%`

  return (
    <WidgetWrapper>
      <Box pb="1.1rem">
          <Typography 
              variant="2"
              component="h2"
              color={"black"}
              fontWeight="600"
          >
              Skills Analysis
          </Typography>
      </Box>
      {
        isLoading ?
        <LoadingWidget />
        :
        <>
        {
          Object.keys(skillData).length > 0
          &&
          <>
          <Divider />
          <Box width="100%" minHeight={300} height={'100%'}>
            <BarChart 
                layout='horizontal'
                height={500}
                series={
                  Object
                  .entries(skillData)
                  .filter(([key, value]) => {void(key); return value !== 0;})
                  .map(([key, value], index) => {
                  return ({
                    label: key, data: [value], color: colours[index], valueFormatter
                  })
                })}

                barGapRatio={0.2}
                margin={isNonMobileScreen ? { right: 275 } : null}
                slotProps={
                  isNonMobileScreen
                  ?
                  {
                    legend: {
                      direction: 'column',
                      position: { vertical: 'middle', horizontal: 'right' },
                      overflow: 'hidden'
                    }
                  }
                  :
                  {
                    legend: {
                      hidden: true
                    }
                  }
                }
                leftAxis={null}
              />
          </Box>
          </>
        }
        </>
      }
    </WidgetWrapper>
  );
};

export default ProfileSkillsWidget;

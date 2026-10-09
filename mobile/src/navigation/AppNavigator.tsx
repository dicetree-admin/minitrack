import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Screens
import SplashScreen from '../screens/SplashScreen';
import MainScreen from '../screens/MainScreen';
import BallTrackingScreen from '../screens/BallTrackingScreen';
import VideoGalleryScreen from '../screens/VideoGalleryScreen';
import SwingRecordingScreen from '../screens/SwingRecordingScreen';
import ResultScreen from '../screens/ResultScreen';

// Types
export type RootStackParamList = {
  Splash: undefined;
  MainTabs: undefined;
  BallTracking: undefined;
  SwingRecording: undefined;
  Result: {
    processingId: string;
    videoUrl: string;
  };
};

export type MainTabParamList = {
  Home: undefined;
  Gallery: undefined;
  Profile: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();

const MainTabs = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: string;

          if (route.name === 'Home') {
            iconName = 'home';
          } else if (route.name === 'Gallery') {
            iconName = 'video-library';
          } else if (route.name === 'Profile') {
            iconName = 'person';
          } else {
            iconName = 'help';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#2E7D32',
        tabBarInactiveTintColor: 'gray',
        headerShown: false,
      })}
    >
      <Tab.Screen 
        name="Home" 
        component={MainScreen}
        options={{
          tabBarLabel: 'Home',
        }}
      />
      <Tab.Screen 
        name="Gallery" 
        component={VideoGalleryScreen}
        options={{
          tabBarLabel: 'My Swings',
        }}
      />
      <Tab.Screen 
        name="Profile" 
        component={MainScreen} // Placeholder
        options={{
          tabBarLabel: 'Profile',
        }}
      />
    </Tab.Navigator>
  );
};

const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator 
        initialRouteName="Splash"
        screenOptions={{
          headerShown: false,
        }}
      >
        <Stack.Screen name="Splash" component={SplashScreen} />
        <Stack.Screen name="MainTabs" component={MainTabs} />
        <Stack.Screen 
          name="BallTracking" 
          component={BallTrackingScreen}
          options={{
            headerShown: true,
            title: 'Ball Tracking',
            headerStyle: {
              backgroundColor: '#2E7D32',
            },
            headerTintColor: '#fff',
          }}
        />
        <Stack.Screen 
          name="SwingRecording" 
          component={SwingRecordingScreen}
          options={{
            headerShown: true,
            title: 'Swing Recording',
            headerStyle: {
              backgroundColor: '#2E7D32',
            },
            headerTintColor: '#fff',
          }}
        />
        <Stack.Screen 
          name="Result" 
          component={ResultScreen}
          options={{
            headerShown: true,
            title: 'Result',
            headerStyle: {
              backgroundColor: '#2E7D32',
            },
            headerTintColor: '#fff',
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
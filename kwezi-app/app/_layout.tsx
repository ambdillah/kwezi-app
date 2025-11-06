import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { UserProvider } from '../contexts/UserContext';

export default function RootLayout() {
  return (
    <UserProvider>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="index" />
        <Stack.Screen name="learn" />
        <Stack.Screen name="games" />
        <Stack.Screen name="progress" />
        <Stack.Screen name="admin" />
        <Stack.Screen name="badges" />
        <Stack.Screen name="offline" />
        <Stack.Screen name="export" />
        <Stack.Screen name="shop" options={{ presentation: 'modal' }} />
      </Stack>
    </UserProvider>
  );
}
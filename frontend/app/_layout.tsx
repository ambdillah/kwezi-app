import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  return (
    <>
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
      </Stack>
    </>
  );
}
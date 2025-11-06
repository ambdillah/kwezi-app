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
        <Stack.Screen name="mayotte-discovery" />
        <Stack.Screen name="shop" />
        <Stack.Screen name="premium" />
        <Stack.Screen name="privacy-policy" options={{ presentation: 'modal' }} />
        <Stack.Screen name="terms-of-sale" options={{ presentation: 'modal' }} />
        <Stack.Screen name="mentions-legales" options={{ presentation: 'modal' }} />
      </Stack>
    </UserProvider>
  );
}

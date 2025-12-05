import { Layout } from "../components/layout";
import { Button } from "../components/ui/button";
import { TimerSettingScreen } from "@/components/screens/TimerSettingScreen";

export default function Home() {
  return (
    <Layout>
      <TimerSettingScreen />
    </Layout>
  );
}

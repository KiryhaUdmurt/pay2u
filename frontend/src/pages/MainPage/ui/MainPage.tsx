import { ActiveServicesSlider } from "components/ActiveServicesSlider/ActiveServicesSlider";
import { Header } from "components/Header/Header";
import { OnboardingDialog } from "components/OnboardingDialog/OnboardingDialog";
import { SearchBar } from "components/SearchBar/SearchBar";
import { ServicesCategories } from "components/ServicesCategories/ServicesCategories";
import { ServicesList } from "components/ServicesList/ServicesList";
import { SliderOnboarding } from "components/SliderOnboarding/SliderOnboarding";
import { sliderOnboardingData } from "shared/data/sliderOnboarding";

const MainPage = () => {
  return (
    <main>
      <Header path="/" title="Развлекательные сервисы" />
      <SearchBar onSearch={() => {}} />
      <SliderOnboarding slidesData={sliderOnboardingData} />
      <OnboardingDialog />
      <ActiveServicesSlider />
      <ServicesCategories />
      <ServicesList />
    </main>
  );
};

export default MainPage;
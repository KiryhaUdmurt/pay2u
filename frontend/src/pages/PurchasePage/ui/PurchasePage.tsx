import { Suspense, memo } from "react";
import { useParams } from "react-router-dom";
import { Header } from "components/Header/Header";
import { Loader } from "widgets/Loader/Loader";
import { useGetSeparateServiceQuery } from "services/ServicesService";
import { PurchaseGuideDialog } from "components/PurchaseGuideDialog/PurchaseGuideDialog";
import cls from "./PurchasePage.module.scss";

const PurchasePage = memo(() => {
  const { id, subscriptionId } = useParams();
  const { data: service } = useGetSeparateServiceQuery(id || "");

  const chosenPlan = service?.subscriptions?.find(
    (plan) => plan.id === Number(subscriptionId)
  );

  const cashbackPercentage =
    chosenPlan?.price && chosenPlan?.cashback
      ? chosenPlan.price / chosenPlan.cashback
      : 0;

  console.log(chosenPlan);
  return (
    <Suspense fallback={<Loader />}>
      <main className={cls.PurchasePage}>
        <Header path={`/services/${id}`} title="Оформление" />
        <div className={cls.title}>
          <img src={service?.image} alt="logo" />
          <h2>{service?.name}</h2>
        </div>
        <p className={cls.subscription}>{chosenPlan?.name}</p>
        <div className={cls.priceContainer}>
          <p className={cls.price}>{chosenPlan?.price} ₽</p>
          <p className={cls.cashback}>
            Кешбэк {cashbackPercentage}₽
          </p>
        </div>
        <p className={cls.paymentMethod}>СПОСОБ ОПЛАТЫ</p>
        <PurchaseGuideDialog />
      </main>
    </Suspense>
  );
});

export default PurchasePage;

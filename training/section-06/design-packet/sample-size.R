# Teaching assumptions, not estimates from a published study or a pilot.
# Two independent, equal-sized normal populations with common SD.
dir.create('r-output',showWarnings=FALSE)
alpha <- 0.05
target <- 0.80
score_sd <- 10
deltas <- c(4,6,8)
retention <- 0.90
rows <- lapply(deltas,function(delta) {
  n <- power.t.test(delta=delta,sd=score_sd,sig.level=alpha,power=target,
                    type='two.sample',alternative='two.sided',strict=TRUE,tol=1e-10)$n
  rounded <- ceiling(n)
  achieved <- power.t.test(n=rounded,delta=delta,sd=score_sd,sig.level=alpha,
                          type='two.sample',alternative='two.sided',strict=TRUE)$power
  previous <- power.t.test(n=rounded-1,delta=delta,sd=score_sd,sig.level=alpha,
                          type='two.sample',alternative='two.sided',strict=TRUE)$power
  # Independently integrate over the chi-square variance term.
  nu <- 2*rounded-2
  critical <- qt(1-alpha/2,df=nu)
  ncp <- delta/score_sd*sqrt(rounded/2)
  integrated <- integrate(function(v) {
    boundary <- critical*sqrt(v/nu)
    (pnorm(-boundary-ncp)+pnorm(ncp-boundary))*dchisq(v,df=nu)
  },lower=qchisq(1e-12,df=nu),upper=qchisq(1-1e-12,df=nu),rel.tol=1e-9)$value
  if(abs(integrated-achieved)>=1e-7)stop(sprintf('Integration mismatch delta=%s: %.12f versus %.12f',delta,integrated,achieved))
  stopifnot(achieved >= target,previous < target)
  data.frame(delta_points=delta,assumed_sd=score_sd,standardized_difference=delta/score_sd,
             alpha=alpha,target_power=target,n_unrounded_per_arm=n,n_required_per_arm=rounded,
             power_at_required_n=achieved,power_at_one_fewer=previous,
             power_by_independent_integration=integrated,
             assumed_retention=retention,recruit_per_arm=ceiling(rounded/retention))
})
results <- do.call(rbind,rows)
stopifnot(identical(as.integer(results$n_required_per_arm),c(100L,45L,26L)))
write.csv(results,'r-output/sample-size.csv',row.names=FALSE,fileEncoding='UTF-8')
# Capacity plan for the 6-point teaching scenario. No participant has been recruited.
selected <- results[results$delta_points==6,]
recruit_total <- 2L*selected$recruit_per_arm
capacity <- data.frame(required_completed_per_arm=selected$n_required_per_arm,
                       recruit_per_arm=selected$recruit_per_arm,recruit_total=recruit_total,
                       scheduled_measurement_rounds=3L,measurement_slots=recruit_total*3L,
                       primary_score_raters=2L,primary_paper_rating_assignments=recruit_total*2L,
                       expected_completed_total=2L*selected$n_required_per_arm)
stopifnot(capacity$recruit_total==100,capacity$measurement_slots==300,
          capacity$primary_paper_rating_assignments==200)
write.csv(capacity,'r-output/resource-capacity.csv',row.names=FALSE,fileEncoding='UTF-8')
writeLines(capture.output(sessionInfo()),'r-output/session-info.txt')
